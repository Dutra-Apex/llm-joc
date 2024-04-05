import math
import argparse
import pandas as pd
import mistral_model as mistral
from youtube_transcript_api import YouTubeTranscriptApi

model = mistral.model
tokenizer = mistral.tokenizer
text_generation_pipeline = mistral.text_generation_pipeline
llm = mistral.llm


def get_section_frames(df, section_minutes = 10, back_time_secs = 0):
  section_length = section_minutes * 60
  end_time = df["start"].max()
  n_sections = math.ceil(end_time / section_length)
  section_list = []
  for i in range(n_sections):
    section_df = df[(df["start"]> i* section_length - back_time_secs) & (df["start"] < (i+1)*section_length)]
    section_list.append(section_df)
  return section_list


def get_text_from_frames(df_list):
  sections_text = []
  for df in df_list:
    section_text = ''
    for index, row in df.iterrows():
      section_text += row["text"] + " "
    sections_text.append(section_text)
  return sections_text
     

def get_section_summary_from_video_id(video_id, section_minutes):
    srt = YouTubeTranscriptApi.get_transcript(video_id)
    video_df = pd.DataFrame(srt, columns=["start", "text"])
    print("Sucessfully obtained transcript from video!")
    sect_list = get_text_from_frames(get_section_frames(video_df, section_minutes = section_minutes))
    summaries = []
    for context in sect_list:
        prompt = f"""[INSTRUCT] Summarize the following video transcript into a concise paragraph.

        {context}

        [/INSTRUCT]
        """
        summary = llm(prompt)
        summaries.append(summary)
    print(f"Generated a summary for every {section_minutes} of video.")
    return summaries


def get_general_summary_from_sections(sections):
   combined_summary = "\n".join(sections)
   GENERAL_SUMMARY_PROMPT = f"""[INSTRUCT] Summarize the following compiled summaries in a concise paragraph.

    {combined_summary}

    [/INSTRUCT]
    """
   
   complete_summary = llm(GENERAL_SUMMARY_PROMPT)
   print("Generated a summary of the whole video.")
   return complete_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pushes text file to vector database and uses it to")
    parser.add_argument("--video_id", help="Youtube video id", default="") 
    parser.add_argument("--output_path")
    parser.add_argument("--section_minutes", default=10)
    args = parser.parse_args()

    video_id = args.video_id
    dest = args.output_path
    section_minutes = args.section_minutes

    section_summaries = get_section_summary_from_video_id(video_id, 10)
    general_summary = get_general_summary_from_sections(section_summaries)

    final_text = f"General summary of the video: \n {general_summary} \n Section Summaries: \n"
    for i in range(len(section_summaries)):
        final_text += f"{i*section_minutes} - {(i+1)*section_minutes} minutes. {section_summaries[i]} \n"
    
    filename = f"video_summary_{video_id}.txt"
    with open(filename, "w") as file:
        file.write(final_text)

    print("Summary sucessfully written")

