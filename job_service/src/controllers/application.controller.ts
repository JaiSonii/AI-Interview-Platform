import type { Request, Response } from "express";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const getApplication = async (req: Request, res: Response) => {
    try {
        const applicationId = req.params.applicationId;
        if (!applicationId) {
            res.status(400).json({ error: "Application ID is required" });
            return;
        }
        const application = await prisma.application.findFirst({
            where: { id: applicationId },
            include: {
                job: true
            }
        })
        return res.status(200).json({ application });
    } catch (error) {
        console.error("Error fetching application:", error);
        res.status(500).json({ error: "Failed to fetch application" });
    }
}