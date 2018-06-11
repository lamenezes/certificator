from certificator import CSVCertificator

certificator = CSVCertificator(delimiter=';', filename_format='eventful-event-{name}.pdf')
certificator.generate()
