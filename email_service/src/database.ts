import { PrismaClient } from "@prisma/client";

class DB{
    private client: PrismaClient | null = null

    constructor(){
        this.client = new PrismaClient()
    }
}

export default new DB();