import { Router } from "express";
import { getApplication } from "../controllers/application.controller";

const router = Router();
router.get('/:applicationId', getApplication); // Not sure of authentication here

export default router