import { Router } from "express";
import { createJob, inviteCandidate } from "../controllers/job.controller";
import { authenticate } from "../middlewares/auth.middleware";

const router = Router();
router.post('/', authenticate, createJob)
router.post('/:jobId/invite', authenticate, inviteCandidate);

export default router