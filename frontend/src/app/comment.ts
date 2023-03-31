export interface Comment {
    id: number;
    commenter: number;
    post: number;
    replies: Comment[];
    text: string;
    created: Date;
}
    