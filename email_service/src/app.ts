import dotenv from 'dotenv'
dotenv.config()

import rabbitmq from './rabbitmq';
import db from './database';

async function startWorker() {
    try {
        console.log("🚀 Starting Email Worker...");

        // Ensure DB connection
        await db.connect()
        await rabbitmq.startConsuming();

        console.log("Worker is running and waiting for messages.");

        // Optional: Handle graceful shutdown
        process.on('SIGINT', async () => {
            console.log("Shutting down...");
            await db.disconnect();
            process.exit(0);
        });

    } catch (error) {
        console.error("❌ Worker failed to start:", error);
        process.exit(1);
    }
}

startWorker();