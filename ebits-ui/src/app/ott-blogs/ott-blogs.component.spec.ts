import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OttBlogsComponent } from './ott-blogs.component';

describe('OttBlogsComponent', () => {
  let component: OttBlogsComponent;
  let fixture: ComponentFixture<OttBlogsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OttBlogsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OttBlogsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
