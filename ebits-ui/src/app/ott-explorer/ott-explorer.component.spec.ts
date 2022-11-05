import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OttExplorerComponent } from './ott-explorer.component';

describe('OttExplorerComponent', () => {
  let component: OttExplorerComponent;
  let fixture: ComponentFixture<OttExplorerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OttExplorerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OttExplorerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
