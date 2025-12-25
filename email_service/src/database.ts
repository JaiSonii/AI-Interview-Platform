import { PrismaClient } from "../generated/prisma/client";
import { PrismaPg } from '@prisma/adapter-pg'
import { MessagePayload } from "./models";
import { config } from "./config";

class DB {
    private client: PrismaClient;
    private adapter;

    constructor() {
        this.adapter = new PrismaPg({ connectionString: config.dbUrl })
        this.client = new PrismaClient({ adapter: this.adapter });
    }

    async connect() {
        await this.client.$connect();
    }

    async disconnect() {
        await this.client.$disconnect();
    }

    async get_application_by_id(application_id: string) {
        return this.client.application.findUnique({
            where: { id: application_id },
            include: {
                job: {
                    include: {
                        organization: true,
                    },
                },
            },
        });
    }

    async updateStatus(payload: MessagePayload) {
        const { application_id, email_type } = payload;

        const status =
            email_type === "invite"
                ? "INVITED"
                : email_type === "completed"
                    ? "COMPLETED"
                    : null;

        if (!status) {
            throw new Error(`Invalid Email Type: ${email_type}`);
        }

        return this.client.application.update({
            where: { id: application_id },
            data: { status },
        });
    }
}

export default new DB();
