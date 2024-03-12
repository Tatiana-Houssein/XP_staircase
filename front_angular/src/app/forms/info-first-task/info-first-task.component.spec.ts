import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoFirstTaskComponent } from './info-first-task.component';

describe('InfoFirstTaskComponent', () => {
  let component: InfoFirstTaskComponent;
  let fixture: ComponentFixture<InfoFirstTaskComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InfoFirstTaskComponent]
    });
    fixture = TestBed.createComponent(InfoFirstTaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
