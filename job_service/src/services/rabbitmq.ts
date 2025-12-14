import amqp from "amqplib";

class RabbitMQ {
    private conn: amqp.ChannelModel | null = null;
    private channel: amqp.Channel | null = null;
    private connUrl: string;

    constructor(url: string) {
        this.connUrl = url;
    }

    async connect() {
        try {
            console.log("Connecting to RabbitMQ...");
            this.conn = await amqp.connect(this.connUrl);
            this.channel = await this.conn.createChannel();
            
            await this.channel.assertExchange('interview.exchange', 'direct', { durable: true });
            console.log("Connected to RabbitMQ");
        } catch (error) {
            console.error("RabbitMQ Connection Failed:", error);
            throw error;
        }
    }

    async send<T extends object>(exchangeName: string, routingKey: string, payload: T): Promise<boolean> {
        if (!this.channel) {
            console.error("Cannot send message: Channel is not initialized. Call connect() first.");
            return false;
        }

        try {
            const sent = this.channel.publish(
                exchangeName,
                routingKey,
                Buffer.from(JSON.stringify(payload)),
                {
                    persistent: true,
                    contentType: 'application/json'
                }
            );

            if (sent) {
                console.log(`[x] Sent to '${routingKey}':`, JSON.stringify(payload).substring(0, 50) + "...");
                return true;
            } else {
                console.error('[!] Buffer full, message dropped.');
                return false;
            }
        } catch (error) {
            console.error("Error publishing message:", error);
            return false;
        }
    }

    async close() {
        await this.channel?.close();
        await this.conn?.close();
    }
}

let instance: RabbitMQ | null = null;

export const initRabbitMQ = async () => {
    if (instance) {
        return instance;
    }

    const url = process.env.RABBITMQ_URL;
    if (!url) {
        throw new Error("RABBITMQ_URL environment variable is missing");
    }

    instance = new RabbitMQ(url);
    await instance.connect();
    return instance;
};

export const getRabbitMQ = (): RabbitMQ => {
    if (!instance) {
        throw new Error("RabbitMQ not initialized. Call initRabbitMQ() in your main.ts first.");
    }
    return instance;
};