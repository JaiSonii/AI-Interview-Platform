import amqp from 'amqplib';
import { config } from './config';
import db from "./database"

class RabbitMQ {
    private conn: amqp.ChannelModel | null = null
    private channel: amqp.Channel | null = null
    private connected: boolean = false
    db = null
    constructor() {
        this.connected = false
    }

    private async setup() {
        this.conn = await amqp.connect(config.rabbitUrl);
        this.channel = await this.conn.createChannel();
        await this.channel.assertExchange('interview.email', 'direct');
        await this.channel.assertQueue(config.queueName, { durable: true });
    }

    async startConsuming(){
        if(!this.connected){
            await this.setup()
        }

        this.channel?.consume(config.queueName, this.processMessage)
    }

    async processMessage(message : amqp.ConsumeMessage | null){
        try {
            // process message here
        } catch (error) {
            
        }   
    }
}

export default new RabbitMQ()