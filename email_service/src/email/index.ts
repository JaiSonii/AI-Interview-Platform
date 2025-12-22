import fs from "fs";
import path from "path";
import nodemailer from 'nodemailer';
import { config } from '../config';


class Mailer {
    private transporter: nodemailer.Transporter | null = null;

    constructor() {
        this.transporter = nodemailer.createTransport({
            host: config.smtp.host,
            port: config.smtp.port,
            secure: true,
            auth: {
                user: config.smtp.user,
                pass: config.smtp.pass
            }
        })
    }

    static renderTemplate(
        name: string,
        variables: Record<string, string>
    ): string {
        const templatePath = path.join(
            __dirname,
            "templates",
            `${name}.html`
        );

        let html = fs.readFileSync(templatePath, "utf-8");

        for (const [key, value] of Object.entries(variables)) {
            html = html.replaceAll(`{{${key}}}`, value);
        }

        return html;
    }

    async send(recieverAddress: string, typ : string, vars: Record<string, string>) {
        const info = await this.transporter?.sendMail({
            from: config.smtp.user,
            to: recieverAddress,
            subject: 'Interview Invitation',
            html: Mailer.renderTemplate(typ, vars)
        })

        return info
    }
}

export default new Mailer()

