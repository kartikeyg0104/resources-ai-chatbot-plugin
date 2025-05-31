export interface Message {
    id: string;
    sender: Sender;
    text: string;
}

export type Sender = 'user' | 'jenkins-bot';
