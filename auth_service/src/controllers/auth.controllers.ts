import type { Request, Response } from "express";
import { loginUser, registerOrganization } from "../services/auth.service";
import { z } from "zod";


const registerSchema = z.object({
    companyName: z.string().min(3, "Company name must be at least 3 characters long"),
    email: z.email("Invalid email format"),
    password: z.string().min(6, "Password must be at least 6 characters long")
})

const loginSchema = z.object({
    email: z.email(),
    password: z.string()
})

export const register = async (req: Request, res: Response): Promise<void> => {
    try {
        const validatedData = registerSchema.parse(req.body);
        const result = await registerOrganization(validatedData);
        res.status(201).json({
            message: "Organization registered successfully",
            token: result.token,
            user: {
                id: result.user.id,
                email: result.user.email,
                role: result.user.role
            }
        })
    } catch (error: any) {
        if (error instanceof z.ZodError) {
            res.status(400).json({
                error: error
            });
            return;
        }

        if (error.message == "Organization already exists") {
            res.status(409).json({ error: error.message });
            return;
        }
        console.error("Registration Error: ", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}

export const login = async (req: Request, res: Response): Promise<void> => {
    try {
        const { email, password } = loginSchema.parse(req.body);
        const result = await loginUser(email, password);
        res.status(200).json({
            massage: "Login successful",
            token: result.token,
            user: {
                id: result.user.id,
                email: result.user.email,
                role: result.user.role
            }
        })
    } catch (error: any) {
        if (error.message == "Invalid credentials") {
            res.status(401).json({ error: error.message });
            return;
        }
        res.status(500).json({ error: "Internal Server Error" });
    }
}

export const getme = async (req: Request, res: Response): Promise<void> => {
    res.json({ user: req.user });
}