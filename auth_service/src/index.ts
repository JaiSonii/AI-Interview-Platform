import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import helmet from "helmet";

import authRoutes from "./routes/auth.routes";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(helmet());
app.use(express.json());


app.use('/auth', authRoutes);

app.get('/health', (req, res) => {
    res.json({ "status": "OK", message: "auth-service" });
})


app.listen(PORT, () => {
    console.log(`Auth Service is running on port ${PORT}`);
})