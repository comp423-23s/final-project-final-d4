import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NoSearchResultComponent } from './no-search-result.component';

describe('NoSearchResultComponent', () => {
  let component: NoSearchResultComponent;
  let fixture: ComponentFixture<NoSearchResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NoSearchResultComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NoSearchResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
