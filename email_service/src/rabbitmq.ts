import amqp from 'amqplib';
import { config } from './config';
import db from "./database";
import email from './email';
import { MessagePayload } from './models';

class RabbitMQ {
    private conn: amqp.ChannelModel | null = null;
    private channel: amqp.Channel | null = null;
    private connected: boolean = false;

    constructor() {
        this.connected = false;
    }

    private async setup() {
        this.conn = await amqp.connect(config.rabbitUrl);
        this.channel = await this.conn.createChannel();
        await this.channel.assertExchange('interview.email', 'direct');
        await this.channel.prefetch(1);
        await this.channel.assertQueue(config.queueName, { durable: true });
        await this.channel.bindQueue(config.queueName, 'interview.email', 'direct');
    }

    async startConsuming() {
        if (!this.connected) {
            await this.setup();
            this.connected = true;
        }

        this.channel?.consume(config.queueName, async (msg) => {
            await this.processMessage(msg);
        });
    }

    private async sendInvite(payload: MessagePayload) {
        // Check for valid application Id 
        const application = await db.get_application_by_id(payload.application_id);

        if (!application) {
            throw new Error('INVALID_ID');
        }

        // Check for status - Idempotency
        if (application.status === 'INVITED') {
            console.log('Candidate Already Invited');
            return;
        }

        const email_vars = {
            candidate_name: application.candidateName,
            date: new Date().toISOString(),
            time: 'anytime',
            mode: 'virtual',
            position: application.job.role,
            link: application.inviteToken,
            company_name: application.job.organization.name,
            sender_name: 'MY Platform',
            sender_title: 'Hiring Team'
        };

        await email.send(application.candidateEmail, 'invite', email_vars);

        await db.updateStatus(payload);
    }

    async processMessage(message: amqp.ConsumeMessage | null) {
        if (!message) return;

        try {
            const content = message.content.toString();
            console.log(content)
            const payload = JSON.parse(content) as MessagePayload;

            console.log(`Processing event: ${payload.email_type} for ${payload.application_id}`);

            if (payload.email_type === 'invite') {
                await this.sendInvite(payload);
            }

            this.channel?.ack(message);

        } catch (error: any) {
            console.error('Error processing message:', error);

            if (error.message === 'INVALID_ID' || error instanceof SyntaxError) {
                console.error("Critical Data Error - Discarding Message");
                this.channel?.ack(message);
            } else {
                console.error("Transient Error - Requeuing");
                this.channel?.nack(message, false, true);
            }
        }
    }
}

export default new RabbitMQ();