import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filterCompagnies'
})
export class FilterCompagniesPipe implements PipeTransform {
  transform(compagnies: any[]): any[] {
    return compagnies.filter(compagnie => compagnie.postes && compagnie.postes.length > 0);
  }
}
