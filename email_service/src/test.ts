import amqp from 'amqplib';
import { config } from './config'; // Reuse your existing config
import { v4 as uuidv4 } from 'uuid';

async function sendTestMessage() {
    try {
        console.log("🔌 Connecting to RabbitMQ...");
        const conn = await amqp.connect(config.rabbitUrl);
        const channel = await conn.createChannel();
        
        const exchange = 'interview.email';
        const queue = config.queueName; // e.g., 'email_queue'

        await channel.assertExchange(exchange, 'direct');
        await channel.assertQueue(queue, { durable: true });

        // !!! IMPORTANT !!!
        // You MUST replace this with a REAL 'id' from your 'Application' table
        // otherwise the worker will log "Critical Data Error" and discard it.
        const VALID_APPLICATION_ID = "valid-app-id-123"; 

        const payload = {
            application_id: VALID_APPLICATION_ID,
            email_type: 'invite',
        };

        const msgBuffer = Buffer.from(JSON.stringify(payload));

        channel.publish(exchange, 'direct', msgBuffer);
        
        console.log(`✅ Sent 'invite' message for App ID: ${VALID_APPLICATION_ID}`);
        console.log(`Payload:`, payload);

        // Close connection after a brief delay
        setTimeout(() => {
            conn.close();
            process.exit(0);
        }, 500);

    } catch (error) {
        console.error("❌ Error:", error);
        process.exit(1);
    }
}

sendTestMessage();