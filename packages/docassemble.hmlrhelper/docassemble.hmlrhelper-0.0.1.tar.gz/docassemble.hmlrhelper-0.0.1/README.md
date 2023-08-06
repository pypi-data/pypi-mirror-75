# docassemble.hmlrhelper (beta)

A docassemble extension that allows you to submit [HM Land Registry (HMLR) forms](https://www.gov.uk/topic/land-registration/searches-fees-forms) to [DocuSign](https://www.docusign.com) through the [DocuSign API](https://developers.docusign.com/) from inside Docassemble interviews.

If for any reason you can't/don't want to use electronic signatures in certain circumstances, you can also still generate a TR1 for signing 'manually' instead.

This extension makes use of the awesome [docassemble.docusign](https://pypi.org/project/docassemble.docusign/) 
extension created by the lovely people at [Radiant Law](https://radiantlaw.com/).

## Current limitations

This implementation is currently limited to TR1's, and is intended to meet the 
requirements for electronic signatures as set out in the *13.3 Our Requirements* section 
of [Practice guide 8: execution of deeds ](https://www.gov.uk/government/publications/execution-of-deeds/practice-guide-8-execution-of-deeds#our-requirements).

* Works for person to person transfers only. There are different requirements and wording 
if the transfer is being signed by an attorney or company, or at the direction of the transferor.
* HMLR will accept up to four transferees listed on the TR1 ([see guidance](https://www.gov.uk/government/publications/registered-titles-whole-transfer-tr1/guidance-completing-form-tr1-for-the-transfer-of-registered-property)) however:
    * the size of Box 12 (Execution) on the sample TR1 that this interview populates means there is a 
    practical limitation of a maximum of 4 signatories and their and associated witnesses (counting both transferors 
    and transferees and noting that transferres don't always need to sign).
    * A simple way to improve on this would be the use of a template file where Box 12 (Execution) was extended to use 
    the full space available on page three.
* Similarly, addresses are limited to 60 characters in order to fit onto a single line, so you may need to get creative with choosing which address elements are important!    
* The person creating the interview is responsible for ensure unique emial/mobile numbers are used for each signatory. The interview does not perform any checks for duplicates.
* The conveyancer still needs to date the deed at the end of the process and submit it to HMLR 'manually'. 

## Installation & Prerequisites

1. Install [docassemble.docusign](https://pypi.org/project/docassemble.docusign/) first. Follow the setup and testing process within *docassemble.docusign* to ensure that you can push documents into DocuSign for signature successfully.

1. Install this docassemble.hmlrhelper package from within your Docassemble package management screen using the latest stable verison available in PyPi:

    - [docassemble.hmlrhelper on PyPi](#)

## Github Repository
    
**Note:** Only install from the Github Repository if you want to input into the development of the extension: 
    
- [https://github.com/mattpennington/docassemble-hmlrhelper](https://github.com/mattpennington/docassemble-hmlrhelper)


## Configuration & Testing

After you've tested *docassemble.docusign* above, and with the extension still in 
test mode (`test-mode: True`) run the test interview at:

{YOUR SERVER BASE URL}/interview?i=docassemble.hmlrhelper:data/questions/test.yml

1. The interview will allow you to choose to either:
  - push a sample populated TR1 into DocuSign and run through a working demo of the signatory process, or;
  - proceed without signing electronically and just populate the TR1 for signing 'manually' 
1. If you choose to sign electronically: 
  - the DocuSign sandbox will send all emails to the the email address of the DocuSign sandbox user you created when setting up *docassemble.docusign*
  - the test interview asks for a mobile phone number that will be used for all SMS's for the Two Factor Authentication. Please use your own mobile number! :-)
  - as you will be using the same mobile number for every test signatory, you will only be asked to complete 2FA once. In a live scenario the mobile number of each recipient 
    would be different and therefore each unique mobile number provided would have to complete 2FA

## Interview Process within Docassemble

**Ensure you have followed the "Configuration & Testing" guide before you start a real interview**

The TR1 interview is at: {YOUR SERVER BASE URL}/interview?i=docassemble.hmlrhelper:data/questions/tr1.yml

The interview runs as follows:

1. Option to choose whether we are preparing a document for esignature or 'manual' processing (we ask fewer questions if we don't need email addressses and mobile numbers fo esignatures)
1. Capture title number and property address
1. Choose whether the transfeor is transferring with full title guarantee
1. Set the consideration
1. Add any additional provisions
1. Add details of transferrors and their witnesses
1. Choose how many transferees there are
1. The number of transferees and additional provisions determes whether the transferees will be signing the document or not, and therefore how much information we need to capture
1. The document is generated and you have the opportunity to review it and go back and make changes if needed
1. You can then continue, at which stage you are asked to add the details for the person who will be responsible for checking over the document and then doing something with it (e.g. sending it to HMLR)
1. The completed document is pushed to Docusign
1. The workflow in Docassemble is completed, and the process for obtaining signatures is controlled by Docusing (starting with an email to the first transferor asking for a signature)

## Process within Docusign

1. 1st **Transferor** clicks document link in email
1. 1st **Transferor** completes Two Factor Authentication by SMS to access document
1. 1st **Transferor** signs deed
1. 1st **Transferor Witness** clicks document link in email
1. 1st **Transferor Witness** completes Two Factor Authentication by SMS to access document
1. 1st **Transferor Witness** witnesses 1st **Transferor** signature and signs deed
1. (Repeat for all transferors)
1. If **Transferees** need to sign too...
    1. 1st **Transferee** clicks document link in email
    1. 1st **Transferee** completes Two Factor Authentication by SMS to access document
    1. 1st **Transferee** signs deed
    1. 1st **Transferee Witness** clicks document link in email
    1. 1st **Transferee Witness** completes Two Factor Authentication by SMS to access document
    1. 1st **Transferee Witness** witnesses 1st **Transferee** signature and signs deed
    1. (Repeat for all transferees)
1. The conveyancer is asked to review and approve the document

## Going Live

In order to put this interview live, you will need to set test mode to false (`test-mode: False`)
in your the configuration for *docassemble.docusign*. You may also need to follow the steps to move 
your application out of the Sandbox and into Docusign's live environment if you haven't done this 
for other documents submitted using *docassemble.docusign* already. Check out the *docassemble.docusign*
documentation to find out how to do this.

## Future Possible Improvements

* Using the HMLR API to lookup the property address/reference, though arguably the conveyancer should have these details to hand anyway 
so perhaps keying them in saves possible lookup errors at this stage. Equally pulling the data from a case management 
system would be great too.
* allow the buyer/seller to add their own witness details and invite them when the document 
reaches them and before they undertake the signing.
* Whilst this implementation of the helper uses Docusign's SMS functionality for Recipient Identity Authentication, its worth noting that Phone Authentication could be made available too for signatories/witnesses that are unable to receive SMS.
* Docusign also supports Knowledge-Based Authentication (KBA) which might prove useful in future.
* HMLR are looking to a future beyond Witnessed electronic signatures to [Qualified electronic signatures](https://www.gov.uk/government/news/hm-land-registry-to-accept-electronic-signatures), therefore further extension through Docusign may be needed in future.
* The implementation uses Signer Recipients rather than Witness Recipients in Docusign for the witness signatures 
as (at the time this version was published) *docassemble.docusign* doesn't have support for [Witness Recipients](https://developers.docusign.com/esign-rest-api/reference/Envelopes/EnvelopeRecipients/#witness-recipient)

## Disclaimer

This is a beta version and as such may contain bugs/unexpected output.

## Software License & Copyright Notice

Copyright (c) 2020 Matt Pennington - Tonic Workflows

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## TR1 Copyright Notice

The *Transfer of whole of registered titles (TR1)* form is (c) Crown copyright (ref: LR/HO).