export class Alert {
  type: string;
  message: string;
  cssClass: string;

  constructor(type?: string, message?: string) {
    this.type = type;
    this.message = message;
    this.cssClass = '';
  }

  inError(): boolean {
    return this.type === 'error';
  }

  notClear(): boolean {
    return this.type !== 'none';
  }

}
