import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BestInStoryComponent } from './best-in-story.component';

describe('BestInStoryComponent', () => {
  let component: BestInStoryComponent;
  let fixture: ComponentFixture<BestInStoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BestInStoryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BestInStoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
