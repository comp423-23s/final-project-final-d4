import { Component, ElementRef, Inject, OnInit, ViewChild } from '@angular/core';
import { FormControl, NgForm } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ProfileService, Profile } from '../profile/profile.service';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatChipInputEvent } from '@angular/material/chips';
import { ENTER, COMMA } from '@angular/cdk/keycodes';
import { PostsService } from '../post.service';

export interface UpdatedPost {
  id: number;
  title: string | null;
  description: string | null;
  content: string | null;
  tags: string[] | null;
}

@Component({
  selector: 'app-post-edit-dialog',
  templateUrl: './post-edit-dialog.component.html',
  styleUrls: ['./post-edit-dialog.component.css'],
})
export class PostEditDialogComponent implements OnInit {
  separatorKeysCodes: number[] = [ENTER, COMMA];
  tagCtrl = new FormControl('');
  filteredTags!: Observable<string[]>;
  tags: string[] = [];
  allTags: string[] = ['Finding teammates', 'Project', 'Bug', 'Frontend', 'Backend'];

  public profile$: Observable<Profile | undefined>;

  @ViewChild('tagInput') tagInput!: ElementRef<HTMLInputElement>;

  constructor(
    public dialogRef: MatDialogRef<PostEditDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: UpdatedPost,
    private profileService: ProfileService,
    public postService: PostsService
  ) {
    this.profile$ = profileService.profile$;
    this.filteredTags = this.tagCtrl.valueChanges.pipe(
      startWith(null),
      map((tag: string | null) => (tag ? this._filter(tag) : this.allTags.slice()))
    );
  }

  ngOnInit(): void {}
  
  save():void{

  }

  cancel(): void{

  }
  // save(form: NgForm): void {
  //   let id = this.data.id;
  //   let title = form.value.title ?? '';
  //   let description = form.value.description ?? '';
  //   let content = form.value.content ?? '';

  //   this.postService
  //     .updatePost(id, title, description, content, this.tags)
  //     .subscribe({
  //       next: (post) => {
  //         console.log('Post updated successfully: ', post);
  //         this.dialogRef.close(post);
  //       },
  //       error: (err) => {
  //         console.error('Error updating post: ', err);
  //       },
  //     });
  // }

  // cancel(): void {
  //   this.dialogRef.close();
  // }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    if (value) {
      this.tags.push(value);
    }

    event.chipInput!.clear();

    this.tagCtrl.setValue(null);
  }

  remove(tag: string): void {
    const index = this.tags.indexOf(tag);

    if (index >= 0) {
      this.tags.splice(index, 1);
    }
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    this.tags.push(event.option.viewValue);
    this.tagInput.nativeElement.value = '';
    this.tagCtrl.setValue(null);
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.allTags.filter((tag) => tag.toLowerCase().includes(filterValue));
  }
}
