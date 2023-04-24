import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NoSearchStringComponent } from './no-search-string.component';

describe('NoSearchStringComponent', () => {
  let component: NoSearchStringComponent;
  let fixture: ComponentFixture<NoSearchStringComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NoSearchStringComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NoSearchStringComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
