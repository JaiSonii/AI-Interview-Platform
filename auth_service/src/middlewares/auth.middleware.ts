import type { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken"

interface AuthPayload {
    userId: string;
    role: string;
    orgId: string;
}

declare global {
    namespace Express {
        interface Request {
            user?: AuthPayload;
        }
    }
}

export const authenticate = (req: Request, res: Response, next: NextFunction): void => {
    const authHeader = req.headers.authorization;
    if(!authHeader || !authHeader.startsWith("Bearer ")) {
        res.status(401).json({ error: "Access Denied, No token provided" });
        return;
    }

    const token = authHeader.split(" ")[1];

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET || "secret")
        req.user = decoded as AuthPayload;
        next();
    } catch (error) {
        res.status(403).json({ error: "Invalid or expired token" });
        return;
    }
}