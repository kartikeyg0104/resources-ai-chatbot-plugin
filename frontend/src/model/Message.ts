export interface Message {
    id: number;
    sender: 'user' | 'jenkins-bot';
    text: string;
}