This folder allows one to create the pTT mapping in the optical links between Stage 1 and Stage 2

Programs :
  - S1_pTT_Mapping : create the mapping viewed as the output of a single Stage 1 board. It produces two files : one for the "directs" links (links between boards of the same sector), and one for the "duplication" links  (links between boards of different sectors)
  - S2_pTT_Mapping : create the mapping viewed as the input of a single Stage 2 board. It produces two files : one for the "directs" links (links between boards of the same sector), and one for the "duplication" links  (links between boards of different sectors)
  - XML_to_firmware_format : convert the results (in xml format) to a text format used for the development of packer/unpacker


Results :
Mappings for a Stage 1 (or Stage 2) board for each sector (and each scenario : 20 * 24 or 20 * 28 pTTs per sector)
