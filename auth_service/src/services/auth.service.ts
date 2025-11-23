import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

const prisma = new PrismaClient();

interface RegisterOrgInput {
    companyName: string;
    email: string;
    password: string;
}

export const registerOrganization = async (input: RegisterOrgInput) => {
    const { companyName, email, password } = input;

    const existingOrg = await prisma.user.findUnique({
        where: { email },
    })

    if (existingOrg) {
        throw new Error("Organization already exists");
    }
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const result = await prisma.$transaction(async (tx) => {
        const newOrg = await tx.organization.create({
            data: {
                name: companyName
            }
        });

        const newUser = await tx.user.create({
            data: {
                email,
                password_hash: hashedPassword,
                role: "ORG_ADMIN",
                organizationId: newOrg.id
            }
        });

        return { newOrg, newUser };
    })

    const token = jwt.sign(
        { userId: result.newUser.id, role: result.newUser.role, orgId: result.newOrg.id },
        process.env.JWT_SECRET || "secret",
        { expiresIn: "1d" }
    )
    return { user: result.newUser, org: result.newOrg, token };
}

export const loginUser = async (email: string, password: string) => {
    const user = await prisma.user.findUnique({
        where: { email }
    });

    if (!user) {
        throw new Error("Invalid credentials");
    }

    const ismatch = await bcrypt.compare(password, user.password_hash);
    if (!ismatch) {
        throw new Error("Invalid credentials");
    }
    const token = jwt.sign(
        { userId: user.id, role: user.role, orgId: user.organizationId },
        process.env.JWT_SECRET || "secret",
        { expiresIn: "1d" }
    )

    return { user, token };
}