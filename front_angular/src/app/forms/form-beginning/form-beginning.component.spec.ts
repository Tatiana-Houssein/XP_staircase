import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormBeginningComponent } from './form-beginning.component';

describe('FormBeginningComponent', () => {
  let component: FormBeginningComponent;
  let fixture: ComponentFixture<FormBeginningComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FormBeginningComponent]
    });
    fixture = TestBed.createComponent(FormBeginningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
