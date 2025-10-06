import argparse
import time
from openai import OpenAI


def create_video_job(client: OpenAI, prompt: str):
    """Create a video generation job with the given prompt."""
    print(f"Creating video with prompt: {prompt}")
    video = client.videos.create(prompt=prompt)
    print(f"Video job created with ID: {video.id}")
    return video


def wait_for_completion(client: OpenAI, video_id: str, poll_interval: int = 5):
    """Poll the video status until it's completed or failed."""
    video = client.videos.retrieve(video_id)
    print(f"Initial status: {video.status}")
    
    while video.status != "completed":
        if video.status == "failed":
            error_msg = f"Video generation failed: {video.error}"
            print(error_msg)
            raise Exception(error_msg)
        
        print(f"Status: {video.status}, Progress: {video.progress}%")
        time.sleep(poll_interval)
        video = client.videos.retrieve(video_id)
    
    print(f"Video completed! Status: {video.status}")
    return video


def download_video(client: OpenAI, video_id: str, output_path: str = "video.mp4"):
    """Download the generated video and save it to a file."""
    print(f"Downloading video {video_id}...")
    response = client.videos.download_content(video_id=video_id)
    content = response.read()
    
    with open(output_path, "wb") as f:
        f.write(content)
    
    print(f"Video saved to {output_path}")
    return output_path


def main():
    """Main function to orchestrate video generation."""
    parser = argparse.ArgumentParser(description="Generate a video using OpenAI Sora")
    parser.add_argument("prompt", help="The prompt describing the video to generate")
    parser.add_argument("-o", "--output", default="video.mp4", help="Output file path (default: video.mp4)")
    parser.add_argument("-i", "--interval", type=int, default=5, help="Poll interval in seconds (default: 5)")
    
    args = parser.parse_args()
    
    client = OpenAI()
    
    try:
        # Create video job
        video = create_video_job(client, args.prompt)
        
        # Wait for completion
        wait_for_completion(client, video.id, args.interval)
        
        # Download video
        download_video(client, video.id, args.output)
        
        print("Video generation complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
