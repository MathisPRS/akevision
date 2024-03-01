import { TestBed } from '@angular/core/testing';

import { AlertService } from './alert.service';

describe('AlertService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  xit('should be created', () => {
    const service: AlertService = TestBed.get(AlertService);
    expect(service).toBeTruthy();
  });
});
