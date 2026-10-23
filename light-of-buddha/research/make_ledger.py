from pathlib import Path
import csv,json,datetime
p=Path(__file__).parent
rows=[
('The Leaving','MN 26','Ariyapariyesana','M i 160','departure; Alara Kalama and Uddaka Ramaputta','Parents weep; nighttime horse departure and four sights are not narrated here.'),
('Beneath the Rose-Apple Tree','MN 36','Mahasaccaka','M i 237','austerities; remembered first jhana; nourishment','Rose-apple childhood experience is remembered later; Sujata is not named in this discourse.'),
('Two Paths in the Mind','MN 19','Dvedhavitakka','M i 114','two classes of thought; cowherd simile','A teaching using recollection and similes, not a dated diary.'),
('The Night in the Forest','MN 4','Bhayabherava','M i 16','fear in wilderness; maintaining posture','No inference that all fear is moral failure or that readers should ignore danger.'),
('The Invitation to Teach','SN 6.1','Brahmayacana/Ayacana','S i 136','Brahma Sahampati request; lotus comparison','Canonical supernatural narrative; setting is goatherd banyan, not Bodhi tree.'),
('The Wheel Begins to Turn','SN 56.11','Dhammacakkappavattana','S v 420','middle way; four truths; Kondanna','Traditional first teaching; no independent contemporary transcript.'),
('What We Cannot Command','SN 22.59','Anattalakkhana','S iii 66','five aggregates and not-self','Not-self does not mean people do not exist or deserve no care.'),
('The Mirror and the Water Bowl','MN 61','Ambalatthikarahulovada','M i 414','water dipper; mirror analogy; repeated reflection','Mirror is a comparison; no material mirror need be present.'),
('The Unanswered Arrow','MN 63','Culamalunkyovada','M i 426','Malunkyaputta; poisoned-arrow simile','Arrow victim is hypothetical; this does not reject all intellectual inquiry.'),
('The Strength of Gentleness','MN 21','Kakacupama','M i 122','Vedehika and Kali; speech; saw comparison','Kali is enslaved; do not euphemise coercion. Saw attack is hypothetical.'),
('The Raft Left on the Shore','MN 22','Alagaddupama','M i 130','raft simile following water-snake simile','Raft is a teaching simile; do not discard ethical training before crossing.'),
('The Gift Not Accepted','SN 7.2','Akkosa','S i 161','Akkosaka Bharadvaja insults; unaccepted food','Food and guests illustrate refusal to reciprocate hostility, not a physical returned gift.'),
('Seeds in an Unseen Field','SN 7.11','Kasibharadvaja','S i 171','ploughing; spiritual cultivation; milk rice','Also Sutta Nipata 1.4; includes supernatural milk-rice episode; no anti-farming message.'),
('The Village of Questions','AN 3.65','Kesamutti/Kalama','A i 188','Kesaputta; greed hate delusion; testing consequences','Thai numbering 3.66; not permission to believe anything or disregard wise counsel.'),
('Words Worth Speaking','MN 58','Abhayarajakumara','M i 392','Abhaya; child analogy; true beneficial timely speech','Child choking is hypothetical; alleged pinch trick belongs to commentary, not canonical speech.'),
('The Man Who Stopped','MN 86','Angulimala','M ii 97','bandit encounter; ordination; later stoning','Supernormal inability to catch Buddha is canonical; elaborate teacher conspiracy is later tradition.'),
('The Fire That Knows No Caste','MN 93','Assalayana','M ii 147','birth; conduct; fire from different woods','Rejects inherited spiritual superiority; does not prove social caste disappeared.'),
('A Night in the Potter’s Shed','MN 140','Dhatuvibhanga','M iii 237','Pukkusati in Bhaggava shed; six elements','Pukkusati does not initially recognise Buddha; later killed by cow; no royal biography asserted.'),
('Soma’s Answer','SN 5.2','Soma','S i 129','Soma confronts Mara in Blind Men’s Grove','Canonical mythic encounter; reply belongs to nun Soma, not Buddha.'),
('A King Learns Enough','SN 3.13','Donapaka','S i 81','Pasenadi; Sudassana; eating moderation','Do not equate ancient measures precisely with modern units; no weight-loss medical promise.'),
('Fields of Generosity','SN 42.7','Khettupama/Desana','S iv 314','Asibandhakaputta; three fields; three pots','About generosity and priorities of teaching, not allocation of money; other sects still taught.'),
('Eight Measures of Freedom','AN 8.53','Samkhitta/Gotami','A iv 280','Mahapajapati asks brief guidance; eight tests','Seclusion and simplicity are monastic-context ideals; not neglect of family responsibilities.'),
('Nanda Comes Home to Himself','Ud 3.2','Nanda','Ud 21','homesickness; heavenly nymphs; release','Heaven journey is canonical supernatural narrative; avoid presenting women as intrinsically impure.'),
('The Second Arrow','SN 36.6','Sallatha','S iv 207','bodily and mental pain; two arrows','Hypothetical simile; never imply grief or mental illness is a moral failure.'),
('Victory Without Peace','SN 3.14','Pathamasangama','S i 82','Ajatasattu defeats Pasenadi; victory breeds enmity','Second battle is SN3.15; include only if separately cited.'),
('Five Things to Remember','AN 5.57','Upajjhatthana','A iii 71','aging illness death separation ownership of actions','Instruction for women/men and lay/ordained; surrounding invented characters must be identified.'),
('A Single Fortunate Day','MN 131','Bhaddekaratta','M iii 187','past future present; diligent day and night','Title translation disputed; original illustrative scene must be identified as literary invention.'),
('The Lute String','AN 6.55','Sona','A iii 374','Sona; vina string tension; balanced energy','Vina is ancient Indian string instrument, not modern guitar; bleeding-foot gloss differs by edition.'),
('The Acrobats’ Balance','SN 47.19','Sedaka','S v 168','bamboo acrobats; self and mutual protection','Acrobat story is a teaching illustration; assistant’s gender/translated name varies.'),
('The Last Journey','DN 16','Mahaparinibbana','D ii 72','final journey; Cunda; Ananda; final instructions','Canonical traditional account with supernatural elements; last meal identification uncertain; no firm death year.')]
urls=[]
for i,(title,ref,name,pts,scene,caveat) in enumerate(rows,1):
 kind,num=ref.split(); sc='https://suttacentral.net/'+kind.lower()+num+'/en/sujato'
 if kind=='MN': url=f'https://www.accesstoinsight.org/tipitaka/mn/mn.{int(num):03d}{"x" if num=="21" else ""}.than.html'
 elif kind=='SN': a,b=num.split('.');url=f'https://www.accesstoinsight.org/tipitaka/sn/sn{int(a):02d}/sn{int(a):02d}.{int(b):03d}.than.html'
 elif kind=='AN': a,b=num.split('.');url=f'https://www.accesstoinsight.org/tipitaka/an/an{int(a):02d}/an{int(a):02d}.{int(b):03d}.than.html'
 elif kind=='Ud':url='https://www.accesstoinsight.org/tipitaka/kn/ud/ud.3.02.than.html'
 else:url='https://www.accesstoinsight.org/tipitaka/dn/dn.16.1-6.vaji.html'
 if i in (20,21):url='https://www.dhammatalks.org/suttas/SN/SN'+('3_13' if i==20 else '42_7')+'.html'
 matches=list((p.parent/'manuscript'/'stories').glob(f'{i:02d}*.md'))
 if matches:
  heading=matches[0].read_text(encoding='utf-8').splitlines()[0]
  title=heading.split('. ',1)[-1]
 row={'story_number':i,'story_title':title,'canonical_or_traditional_source':name+' Sutta','precise_textual_reference':ref+'; PTS '+pts+'; '+scene,'buddhist_tradition':'Pali canon preserved in Theravada; early Buddhist discourse tradition','classification':'canonical teaching/simile' if i in (9,10,11,24,26,27,29) else 'canonical traditional narrative; not independently established history','research_url':url,'suttacentral_comparison_url':sc,'source_language':'Pali (English translations consulted; no full philological collation)','translation_and_copyright_status':'Thanissaro Bhikkhu research translation: restricted/noncommercial; not licensed for prose reuse. Sujato Bilara translations CC0 per official LICENSE. DN16 ATI Vajira/Story copyrighted; research only.' if i==30 else 'Thanissaro Bhikkhu: research consultation only; ATI CC BY-NC 4.0; no commercial reuse of English. Sujato Bilara translations CC0 per official LICENSE.','factual_caveats':caveat,'illustration_references':f'artwork/illustration-briefs/{i:02d}.md; research/art-history-references.md','verification_status':'Live English source opened 2026-10-23; identifier and relevant narrative confirmed; manuscript-to-source review separate','access_date':'2026-10-23'}
 urls.append(row)
 (p/'story-sources'/f'{i:02d}.md').write_text('# '+title+'\n\n'+'\n\n'.join('**'+k.replace('_',' ').title()+':** '+str(v) for k,v in row.items())+'\n',encoding='utf-8')
with (p/'source-verification.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=urls[0]);w.writeheader();w.writerows(urls)
(p/'bibliography.md').write_text('# Research bibliography\n\nAccessed 23 October 2026. The following are research references, not permissions to reproduce modern English translations. The manuscript uses original literary retellings of ancient narrative material.\n\n'+ '\n'.join(f'- {r["precise_textual_reference"].split("; ")[0]}. [{r["canonical_or_traditional_source"]}]({r["research_url"]}). English translation consulted; canonical Pali tradition.' for r in urls)+'\n\n## Rights reference\n\n[SuttaCentral Bilara licensing](https://github.com/suttacentral/bilara-data/blob/published/LICENSE.md): Bilara-supported translations CC0. Access to Insight page footers identify Thanissaro translations as CC BY-NC 4.0. Ancient texts and modern translations must not be conflated.\n',encoding='utf-8')
print('Wrote 30 records and bibliography')
