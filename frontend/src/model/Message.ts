export interface Message {
    id: number;
    sender: Sender;
    text: string;
}

export type Sender = 'user' | 'jenkins-bot';
