import {Component, Input, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {DomSanitizer, SafeUrl} from "@angular/platform-browser";

@Component({
  selector: 'app-wav-player',
  templateUrl: './wav-player.component.html',
  styleUrls: ['./wav-player.component.css']
})
export class WavPlayerComponent implements OnInit, OnDestroy {
  @Input() bytes: ArrayBuffer

  @ViewChild('audioPlayer')
  audioPlayerElement

  audioUrl: string | null = null
  audioSafeUrl: SafeUrl | null = null
  isPlaying: boolean = false

  constructor(private domSanitizer: DomSanitizer) {
  }

  ngOnInit(): void {
    const audioBlob1 = new Blob([this.bytes.slice(0, this.bytes.byteLength / 2)], {type: 'audio/wav'})
    this.audioUrl = URL.createObjectURL(audioBlob1)
    this.audioSafeUrl = this.domSanitizer.bypassSecurityTrustUrl(this.audioUrl)
  }

  ngOnDestroy() {
    if (this.audioUrl != null) {
      URL.revokeObjectURL(this.audioUrl)
    }
  }

  clickButton() {
    const audioPlayer = this.audioPlayerElement.nativeElement as HTMLAudioElement
    if (this.isPlaying) {
      audioPlayer.pause()
    } else {
      audioPlayer.play()
    }
  }

  onPlaying() {
    this.isPlaying = true
  }

  onPaused() {
    this.isPlaying = false
  }

  onEnded() {
    this.isPlaying = false
  }
}
