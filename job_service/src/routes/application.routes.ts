import { Router } from "express";
import { getApplication } from "../controllers/application.controller";

const router = Router();
router.get('/application/:inviteToken', getApplication); // Not sure of authentication here

export default router