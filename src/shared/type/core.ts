export type Precision = 'fp32' | 'fp16' | 'bf16'

export interface Final2xCoreConfig {
  config: {
    pretrained_model_name: string
    device: string
    gh_proxy: string | null
    target_scale: number | null
    output_path: string
    input_path: string[]
    use_tile: boolean
    precision: Precision
    save_format: string
  }
  options: {
    open_output_folder: boolean
  }
}
