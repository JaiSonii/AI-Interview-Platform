import { MessagePayload } from "./models";

// Define simpler interfaces just for the mock to avoid huge Prisma dependencies
interface MockApplication {
    id: string;
    candidateEmail: string;
    candidateName: string;
    inviteToken: string;
    status: string;
    job: {
        role: string;
        organization: {
            name: string;
        }
    }
}

class MockDB {
    // In-memory storage to simulate the database table
    private applications: Map<string, MockApplication> = new Map();

    constructor() {
        // SEED DATA: Let's create one valid application for testing.
        // ID: 'valid-app-id-123'
        this.applications.set('valid-app-id-123', {
            id: 'valid-app-id-123',
            candidateEmail: 'your_email@example.com', // Change this to your real email to see the result
            candidateName: 'John Doe',
            inviteToken: 'https://interview.platform.com/magic-token-xyz',
            status: 'DRAFT',
            job: {
                role: 'Senior Backend Engineer',
                organization: {
                    name: 'Tech Corp Inc.'
                }
            }
        });
    }

    async connect() {
        console.log("✅ [MOCK] Database connected (In-Memory)");
    }

    async disconnect() {
        console.log("🔌 [MOCK] Database disconnected");
    }

    async get_application_by_id(application_id: string) {
        console.log(`🔍 [MOCK] Searching for Application ID: ${application_id}`);
        
        const app = this.applications.get(application_id);
        
        // Simulate network delay
        await new Promise(r => setTimeout(r, 100)); 

        if (!app) return null;
        
        return app;
    }

    async updateStatus(payload: MessagePayload) {
        const app = this.applications.get(payload.application_id);
        
        if (!app) {
            throw new Error("Application not found in Mock DB");
        }

        let newStatus = "";
        if (payload.email_type === 'invite') newStatus = 'INVITED';
        else if (payload.email_type === 'completed') newStatus = 'COMPLETED';

        // Update the in-memory object
        app.status = newStatus;
        this.applications.set(payload.application_id, app);

        console.log(`💾 [MOCK] Updated Status for ${payload.application_id} to '${newStatus}'`);
        
        // Return simulated Prisma response
        return { count: 1 };
    }
}

export default new MockDB();