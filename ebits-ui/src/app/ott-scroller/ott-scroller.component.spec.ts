import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OttScrollerComponent } from './ott-scroller.component';

describe('OttScrollerComponent', () => {
  let component: OttScrollerComponent;
  let fixture: ComponentFixture<OttScrollerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OttScrollerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OttScrollerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
