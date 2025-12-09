import express from "express";
import cors from "cors";
import jobRouter from './routes/job.routes'
import applicationRouter from './routes/application.routes'


const app = express();
const PORT = process.env.PORT || 4001;

app.use(cors());
app.use(express.json());
app.use('/jobs', jobRouter);
app.use('/application', applicationRouter)

app.get("/health", (req, res) => {
    res.status(200).send("Job Service is healthy");
})

app.listen(PORT, () => {
    console.log(`Job Service is running on port ${PORT}`);
})