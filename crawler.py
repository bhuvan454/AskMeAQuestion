''' 
Bhuvan Chennoju
@linkedin: https://www.linkedin.com/in/bhuvanchennoju/
===================================================================================================
'''
import os
import sys
import json
import asyncio
from utils import *


async def main():
    args = get_args()
    start_year = args.start_year
    end_year = args.end_year
    output_dir = args.output_dir

    #  parser.add_argument('--type', type=str, choices=['metadata', 'pdf', 'abstract', 'all'],
    #                     default='all', help='Type of data to download (metadata, pdf, abstract, all)')

    download_type = args.type 

    if not os.path.exists(output_dir):
        sys.exit(f"Output directory {output_dir} does not exist")


    for year in range(start_year, end_year + 1):
        year_dir = os.path.join(output_dir, str(year))

        paper_ids, abstract_paths, metadata_paths, pdf_paths = await get_paper_paths(year)

        for paper_id, abstract_path, metadata_path, pdf_path in zip(paper_ids, abstract_paths, metadata_paths, pdf_paths):
            print(f"Downloading {paper_id}")
            
            # save directory for the paper
            save_dir = os.path.join(year_dir, paper_id)
            os.makedirs(save_dir, exist_ok=True)

            if download_type == 'metadata':
                metadata = get_metadata(metadata_path)
                with open(os.path.join(save_dir, f"{paper_id}_metadata.json"), "w") as f:
                    json.dump(metadata, f, indent=4)
                continue

            if download_type == 'pdf':
                pdf = get_pdf(pdf_path)
                with open(os.path.join(save_dir, f"{paper_id}.pdf"), "wb") as f:
                    f.write(pdf)
                continue

            if download_type == 'abstract':
                abstract = get_abstract(abstract_path)
                with open(os.path.join(save_dir, f"{paper_id}_abstract.json"), "w") as f:
                    json.dump(abstract, f, indent=4)
                continue

            if download_type == 'all':
                abstract = get_abstract(abstract_path)
                metadata = get_metadata(metadata_path)
                pdf = get_pdf(pdf_path)
                with open(os.path.join(save_dir, f"{paper_id}_abstract.json"), "w") as f:
                    json.dump(abstract, f, indent=4)

                with open(os.path.join(save_dir, f"{paper_id}_metadata.json"), "w") as f:
                    json.dump(metadata, f, indent=4)

                with open(os.path.join(save_dir, f"{paper_id}.pdf"), "wb") as f:
                    f.write(pdf)
                continue


if __name__ == "__main__":
    asyncio.run(main())
