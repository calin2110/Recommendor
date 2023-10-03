import {Injectable} from '@angular/core';
import {HttpResponse} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class MultipartResponseInterpreterService {
  private readonly CONTENT_DISPOSITION_HEADER = 'Content-Disposition: form-data; name="'
  private readonly CONTENT_TYPE_HEADER = 'Content-Type: '
  private readonly CONTENT_LENGTH_HEADER = 'Content-Length: '
  private readonly CR = 13
  private readonly QUOTE = 34


  constructor() {
  }

  getBoundaryFromResponse(request: HttpResponse<any>): string | null {
    const contentTypeHeader = request.headers.get('Content-Type');
    if (!contentTypeHeader) {
      return null;
    }
    const boundaryRegex = /boundary=(.*)/;
    const match = contentTypeHeader.match(boundaryRegex);
    if (!match) {
      return null;
    }
    return match[1];
  }

  parseMultipartResponse(response: HttpResponse<ArrayBuffer>): Map<string, any> {
    const boundary = this.getBoundaryFromResponse(response)!!
    const items = new Map<string, any>()
    const dataView = new DataView(response.body)
    let idx = 0
    // remove last boundary and its new lines
    const maxLength = dataView.byteLength - boundary.length - 6
    while (idx < maxLength) {
      // skip boundary and new lines
      idx += 4 + boundary.length
      // skip CONTENT_DISPOSITION_HEADER
      idx += this.CONTENT_DISPOSITION_HEADER.length
      let name = ""
      // while not "
      while (dataView.getUint8(idx) !== this.QUOTE) {
        name += String.fromCharCode(dataView.getUint8(idx))
        idx += 1
      }
      // skip "
      idx += 1

      // skip if filename is present
      while (dataView.getUint8(idx) !== this.CR) {
        idx += 1
      }

      // skip new lines
      idx += 2

      // skip `Content-Type: `
      idx += this.CONTENT_TYPE_HEADER.length

      let type = ""
      // while not new line
      while (dataView.getUint8(idx) !== this.CR) {
        type += String.fromCharCode(dataView.getUint8(idx))
        idx += 1
      }

      // skip new lines
      idx += 2

      // skip `Content-Length: `
      idx += this.CONTENT_LENGTH_HEADER.length

      let length_str = ""
      // while not new line
      while (dataView.getUint8(idx) !== this.CR) {
        length_str += String.fromCharCode(dataView.getUint8(idx))
        idx += 1
      }
      const length = parseInt(length_str)

      // skip new lines
      idx += 2
      // there are also some extra new lines to skip
      idx += 2

      // get subarray of array buffer
      const data = dataView.buffer.slice(idx, idx + length)
      idx += length
      idx += 2
      items.set(name, data)
    }

    return items
  }

}
