import json

# This is the clean, valid data
data = {
    "data": {
        "vector_data": [
            {
                "id": 1,
                "text": "Hotels Near Malpani Infertility Clinic: Happy Home Hotel (Rs 1400), Hotel Fortune, Hotel Manama. A 5 min walk away."
            },
            {
                "id": 2,
                "text": "A complete IVF cycle at our clinic costs US $4000. This includes all medical procedures, lab tests, scans, egg pickup and embryo transfer."
            },
            {
                "id": 3,
                "text": "Embryo freezing costs US $1000 per year. Laser assisted hatching costs US $500 more."
            },
            {
                "id": 4,
                "text": "The clinic is located in Colaba, Mumbai. It is about 15 minutes by taxi from VT Station."
            }
        ]
    }
}

# Write this data to the file automatically
filename = 'sample_context_vectors-01.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(f"✅ Success! Created {filename} correctly.")