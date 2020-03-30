# Mailer: examples

This folder contains some examples to demonstrate how to use `mailer`.

To run the example properly, do not just open the `.html` files, but be sure
to server them with a basic HTTP server, for instance:

```
python -m http.server <port>
```

The reason for this requirement is that if you enable CORS protection on `mailer`,
opening files directly in a web-browser will not set the `Origin` header properly,
thus all requests will fail.

Be sure to configure and run an instance of `mailer` before using them!

## Examples:

- [Simple AJAX form](simple-ajax.html)
- [Simple AJAX form with Google ReCaptcha](simple-ajax-recaptcha.html)
