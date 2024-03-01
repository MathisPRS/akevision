import { Component, OnInit } from '@angular/core';
import {UntypedFormBuilder, UntypedFormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-test-mat-material',
  templateUrl: './test-mat-material.component.html',
  styleUrls: ['./test-mat-material.component.scss']
})
export class TestMatMaterialComponent implements OnInit {

  form: UntypedFormGroup;
  timeInterval : number = 5;

  constructor( private formBuilder: UntypedFormBuilder
  ) {
    this.form = this.formBuilder.group({
      startDate: [{ value: '', disabled: true }, Validators.required],
      endDate: [{ value: '', disabled: true }, Validators.required]
    });
  }

  ngOnInit() {
    this.form.get('startDate').setValue(new Date()),
    this.form.get('endDate').setValue(new Date()),
    this.form.get('startDate').enable();
    this.form.get('endDate').enable();
  }

}
