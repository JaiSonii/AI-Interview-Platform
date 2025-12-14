import type { Request, Response } from "express";
import { PrismaClient } from "@prisma/client";
import z from "zod";
import crypto from "crypto";
import { getRabbitMQ } from "../services/rabbitmq";

const prisma = new PrismaClient();

const createJobSchema = z.object({
    role: z.string().min(3),
    description: z.string().min(10),
    exp_range: z.object({
        min_exp : z.number(),
        max_exp: z.number()
    })
});

export const createJob = async (req: Request, res: Response) => {
    try {
        const { role, description, exp_range } = createJobSchema.parse(req.body);

        const orgId = req.user?.orgId;
        if (!orgId) {
            res.status(401).json({ error: "Organization ID is missing" });
            return;
        }
        const job = await prisma.job.create({
            data: {
                role,
                description,
                exp_range,
                organizationId: orgId,
                status: "OPEN",
            }
        })
        const rabbitmq = getRabbitMQ()
        const payload = {
            job_id : job.id
        }
        rabbitmq.send('interview.exchange', 'job.question.create', payload)
        return res.status(201).json({ 'message': 'Job created successfully', job });

    } catch (error) {
        console.error("Error creating job:", error);
        res.status(500).json({ error: "Failed to create Job" });
    }
}

const inviteCandidateSchema = z.object({
    candidateEmail: z.email(),
    candidateName: z.string().min(2)
})

export const inviteCandidate = async (req: Request, res: Response) => {
    try {
        const jobId = req.params.jobId;
        const { candidateEmail, candidateName } = inviteCandidateSchema.parse(req.body);

        const job = await prisma.job.findUnique({
            where: { id: jobId }
        })
        if (!job) {
            res.status(404).json({ error: "Job not found" });
            return;
        }

        if (job.organizationId !== req.user?.orgId) {
            res.status(403).json({ error: "Unauthorized to invite candidates for this job" });
            return;
        }
        const token = crypto.randomBytes(32).toString('hex');

        const application = await prisma.application.create({
            data: {
                candidateEmail,
                candidateName,
                jobId: job.id,
                inviteToken: token,
                status: 'INVITED'
            }
        })
        const inviteLink = `https://localhost:3000/interview/${token}`;
        res.status(201).json({ message: "Candidate invited successfully", inviteLink, applicationId: application.id });
    } catch (error) {
        console.error("Error inviting candidate:", error);
        res.status(500).json({ error: "Failed to invite candidate" });
    }
}