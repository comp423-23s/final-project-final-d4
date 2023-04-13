import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Post, PostsService } from '../post.service';
import { Subscription } from 'rxjs';
import { ProfileService, Profile } from '../profile/profile.service';
import { HttpErrorResponse } from '@angular/common/http';
import {MatAutocompleteSelectedEvent} from '@angular/material/autocomplete';
import {MatChipInputEvent} from '@angular/material/chips';
import {FormControl} from '@angular/forms';
import { Observable, map, startWith } from 'rxjs';
import {COMMA, ENTER} from '@angular/cdk/keycodes';


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
  
  public profile$: Observable<Profile | undefined>;

  constructor(
    public postService: PostsService,
    private profileService: ProfileService
  ) {
    this.profile$ = profileService.profile$,
    this.filteredTags = this.tagCtrl.valueChanges.pipe(startWith(null),
    map((fruit: string | null) => (fruit ? this._filter(fruit) : this.allTags.slice())),
  );
}


  onPost(form: NgForm):void{
    
    let postedBy = parseInt(form.value.id ?? "");
    let title = (form.value.title ?? "");
    let description = (form.value.description ?? "");
    let time = (form.value.dateTime)
    let tag = (form.value.tag ?? "");

    
    form.resetForm()
  }

  private onSuccess(post: Post): void {
    window.alert(`Thanks for posting`);
  }

  private onError(err: HttpErrorResponse) {
    if (err.message) {
      window.alert(err.error.detail);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
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
