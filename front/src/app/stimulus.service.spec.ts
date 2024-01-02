import { TestBed } from '@angular/core/testing';

import { StimulusService } from './stimulus.service';

describe('StimulusService', () => {
  let service: StimulusService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StimulusService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
