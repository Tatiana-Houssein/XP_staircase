import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormEndingComponent } from './form-ending.component';

describe('FormEndingComponent', () => {
  let component: FormEndingComponent;
  let fixture: ComponentFixture<FormEndingComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FormEndingComponent]
    });
    fixture = TestBed.createComponent(FormEndingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
