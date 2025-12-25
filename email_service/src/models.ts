export interface MessagePayload {
    application_id : string,
    email_type: 'invite' | 'reminder' | 'completed',
}