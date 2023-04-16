import { Component } from '@angular/core';
import { PostView, PostsService } from '../post.service';
import { ActivatedRoute } from '@angular/router';
import { CommentService } from '../comment.service';
import { Comment } from '../comment.model';
import { newComment } from '../comment.service';

@Component({
  selector: 'app-post-details',
  templateUrl: './post-details.component.html',
  styleUrls: ['./post-details.component.css']
})
export class PostDetailsComponent {
  post!: PostView;
  comments: Comment[] = [];
  projectId!: number;
  selectedValue!: string;

  constructor(
    private route: ActivatedRoute,
    private postService: PostsService,
    private commentService: CommentService
  ) {}

  ngOnInit(): void {
    const postId = Number(this.route.snapshot.paramMap.get('id'));
    this.postService.getPostById(postId).subscribe((post) => {
      this.post = post;
    });
    this.projectId = postId; 
    this.getComments();
  }

  getComments(): void {
    this.commentService.getComments(this.projectId).subscribe((comments) => {
      this.comments = comments;
    });
  }

  addComment(text: string, isPrivate: string): void {
    this.commentService.addComment(text, this.post.id, isPrivate === 'true').subscribe((comment: Comment) => {
      this.comments.push(comment);
    });
  }

  deleteComment(id: number): void {
    this.commentService.deleteComment(id).subscribe(() => {
      this.comments = this.comments.filter((comment) => comment.id !== id);
    });
  }
}
