import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OttComponent } from './ott.component';

describe('OttComponent', () => {
  let component: OttComponent;
  let fixture: ComponentFixture<OttComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OttComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OttComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
