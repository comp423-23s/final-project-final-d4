import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { PostView, PostsService } from '../post.service';
import { ProfileService, Profile } from '../profile/profile.service';
import { HttpErrorResponse } from '@angular/common/http';
import {MatAutocompleteSelectedEvent} from '@angular/material/autocomplete';
import {MatChipInputEvent} from '@angular/material/chips';
import {FormControl} from '@angular/forms';
import { Observable, catchError, map, startWith } from 'rxjs';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';


@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.css']
})

export class CreatePostComponent {
  separatorKeysCodes: number[] = [ENTER, COMMA];
  tagCtrl = new FormControl('');
  filteredTags!: Observable<string[]>;
  tags: string[] = ['Share insights'];
  allTags: string[] = ['Finding teammates', 'Project', 'Bug', 'Frontend', 'Backend'];
  @ViewChild('tagInput')
  tagInput!: ElementRef<HTMLInputElement>;
  
  
  // declares a public property profile$ that holds an observable of either a Profile object or undefined
  public profile$: Observable<Profile | undefined>;
  
  constructor(
    public postService: PostsService,
    private profileService: ProfileService,
    private formBuilder: FormBuilder,
    private router: Router
  ) {
    //Assigns the profile$ observable from the ProfileService to the component's profile$ property.
    this.profile$ = profileService.profile$,
    //tag section
    this.filteredTags = this.tagCtrl.valueChanges.pipe(startWith(null),
    map((fruit: string | null) => (fruit ? this._filter(fruit) : this.allTags.slice())),
  );
}

  onPost(form: NgForm):void{
    let title = (form.value.title ?? "");
    let description = (form.value.description ?? "");
    let content = (form.value.content ?? "");
    let time = (form.value.dateTime);
    let comments = (form.value.comments ?? "");

    this.postService.addPost(title, description, content, this.tags)
    .subscribe({
      next: (posts) => {
        console.log('Post added successfully: ', posts);
        form.resetForm();
        this.router.navigate(['/projects']);
      },
      error: (err) => {
        console.error('Error creating post: ', err);
      }
    });

  }
  
  
  // For tags part
  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add our tag
    if (value) {
      this.tags.push(value);
    }

    // Clear the input value
    event.chipInput!.clear();

    this.tagCtrl.setValue(null);
  }

  remove(fruit: string): void {
    const index = this.tags.indexOf(fruit);

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

    return this.allTags.filter(tag => tag.toLowerCase().includes(filterValue));
  }


}
