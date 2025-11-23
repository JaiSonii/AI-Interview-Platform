import { Router } from "express";
import { register, login, getme } from "../controllers/auth.controllers";
import { authenticate } from "../middlewares/auth.middleware";

const router = Router();

router.post("/register-org", register);
router.post("/login", login);
router.get('/me',authenticate, getme);

export default router;