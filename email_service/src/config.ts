import 'dotenv/config';

export const config = {
  rabbitUrl: process.env.RABBIT_URL!,
  queueName: process.env.QUEUE_NAME!,
  dbUrl: process.env.DATABASE_URL!,
  smtp: {
    host: process.env.SMTP_HOST!,
    port: Number(process.env.SMTP_PORT),
    user: process.env.SMTP_USER!,
    pass: process.env.SMTP_PASS!
  }
};
